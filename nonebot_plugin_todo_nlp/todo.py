from typing import AnyStr, List
import pandas as pd
import pandas.errors
import os
from nonebot_plugin_htmlrender import template_to_pic
from pandas import DataFrame, read_csv, concat
from datetime import datetime, timedelta
from typing import Union
from re import match
from pathlib import Path
from pandas.errors import EmptyDataError


# TODO:add log

class TodoToken:
    def __init__(self,
                 name: str,
                 start_date: Union[str, datetime, None] = None,
                 end_date: Union[str, datetime, None] = None,
                 priority: Union[int, None] = 3,
                 format_str: str = "%Y-%m-%d"):
        self.format_str = format_str
        self._name = name
        self._start_date = TodoToken.time_parse(start_date, format_str)
        self._end_date = TodoToken.time_parse(end_date, format_str)
        self._priority = priority

    @property
    def name(self):
        return self._name

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def priority(self):
        return self._priority

    @property
    def time_left(self):
        end = datetime.strptime(self.end_date, self.format_str) + timedelta(days=1)
        today = datetime.today()
        time_len = (end - today).days
        return time_len

    @property
    def percentage(self):
        start = datetime.strptime(self.start_date, self.format_str)
        end = datetime.strptime(self.end_date, self.format_str) + timedelta(days=1)
        today = datetime.today()
        time_len = (end - start)
        time_spent = (today - start)
        return int(time_spent / time_len * 100)

    @classmethod
    def time_parse(cls, _time: [str, datetime, None],
                   format_str: str = "%Y-%m-%d"):
        if _time is None:
            _time = datetime.today()
        elif isinstance(_time, datetime):
            _time = _time.strftime(format_str)
        else:
            try:
                test = datetime.strptime(_time, format_str)
            except ValueError:
                raise ValueError("Time parsing failed.")
        return _time

    def __lt__(self, other):
        if not isinstance(other, TodoToken):
            raise ValueError("{other} is not a TodoToken.")
        if self.end_date != other.end_date:
            return self.end_date < other.end_date
        elif self.priority != other.priority:
            return self.priority < other.priority
        elif self.start_date != other.start_date:
            return self.start_date < other.start_date
        else:
            return self.name < other.name

    def __eq__(self, other):
        if not isinstance(other, TodoToken):
            raise ValueError("{other} is not a TodoToken.")
        if (self.name == other.name and
                self.start_date == other.start_date and
                self.end_date == other.end_date and
                self.priority == other.priority):
            return True
        else:
            return False

    def __str__(self):
        return self._name + ',' + self._start_date + ',' + self._end_date + ',' + str(self._priority)

    def to_dict(self):
        return {'name': self._name,
                'start_date': self._start_date,
                'end_date': self._end_date,
                'priority': self._priority}


class TodoList:
    def __init__(self, user: str, path: str, format_str: str = "%Y-%m-%d"):
        self._list = list()
        self._user = user
        self._path = path
        self._format_str = format_str
        try:
            df = read_csv(self.path + '/' + user + ".csv")
        except FileNotFoundError or EmptyDataError:
            df = None
        if df is not None:
            for index, row in df.iterrows():
                token = TodoToken(row['name'], row['start_date'],
                                  row['end_date'], row['priority'], self.format_str)
                self._list.append(token)

    @property
    def size(self):
        return len(self._list)

    @property
    def path(self):
        return self._path

    @property
    def format_str(self):
        return self._format_str

    def add_data(self, token: TodoToken) -> bool:
        if token in self._list:
            return False
        else:
            self._list.append(token)
            self.write_data()
            return True

    def remove_data(self, name: str) -> int:
        list_len = len(self._list)
        self._list = [token for token in self._list if not match(name, token.name)]
        if list_len > len(self._list):
            self.write_data()
        return list_len - len(self._list)

    def change_data(self, name: str, slot: str, content: str):
        count = 0
        if slot == 'priority':
            for token in self._list:
                if match(name, token.name) is not None:
                    token._priority = int(content)
                    count += 1
        else:
            for token in self._list:
                if match(name, token.name) is not None:
                    setattr(token, slot, content)
                    count += 1
        self.write_data()
        return count

    def write_data(self):
        self._list.sort()
        if len(self._list) == 0:
            df = pd.DataFrame(columns=['name', 'start_date', 'end_date', 'priority'])
            df.to_csv(self.path + '/' + self._user + '.csv', index=False)

        else:
            df = DataFrame()
            for token in self._list:
                tmp = DataFrame([token.to_dict()])
                df = concat([df, tmp], axis=0, ignore_index=True)
            df.to_csv(self.path + '/' + self._user + '.csv', index=False)

    async def get_img(self):
        list_by_date: List[(str, int, List[TodoToken])] = list()
        now_date = ""
        date_count = 0
        now_date_token: List[TodoToken] = list()
        for token in self._list:
            if token.end_date != now_date:
                date_count += 1
                now_date = token.end_date
                now_date_token:List[TodoToken] = list()
                list_by_date.append((now_date, token.time_left, now_date_token))
            now_date_token.append(token)

        content_width = 500
        content_height = 76.4 + \
                         34 * date_count + \
                         64 * len(self._list)
        # estimated title_height + date_height + list_token_height
        img_width = content_width / 0.618
        img_height = content_height / 0.618
        template_path = str(Path(__file__).parent / "templates")
        img = await template_to_pic(template_path=template_path,
                                    template_name="template.html",
                                    templates={
                                        "list_by_date": list_by_date,
                                    },
                                    pages={
                                        "viewport": {"width": int(img_width), "height": int(img_height)},
                                        "base_url": f"file://{template_path}"
                                    },
                                    )
        return img


class TodoUtil:
    def __init__(self, user: str, path: str = str(Path(__file__).parent / "todo_data" ), format_str: str = "%Y-%m-%d"):
        if not os.path.exists(path):
            os.makedirs(path)
        self._todo_list: TodoList = TodoList(user, path)
        self._format_str = format_str

    @property
    def format_str(self):
        return self._format_str

    @property
    def list_size(self):
        return self.todo_list.size

    @property
    def todo_list(self):
        return self._todo_list

    def add_data_to_list(self, token: TodoToken):
        return self.todo_list.add_data(token)

    def remove_data(self, name: str):
        return self.todo_list.remove_data(name)

    def change_data(self, name: str, slot: str, content: str):
        return self.todo_list.change_data(name, slot, content)

    def change_time(self, name: str, time: str):
        return self.todo_list.change_data(name, '_end_date', time)

    def finish_job(self, name: str):
        return self.remove_data(name)

    def get_list(self):
        return self.todo_list

    def get_list_img(self):
        return self.todo_list.get_img()
