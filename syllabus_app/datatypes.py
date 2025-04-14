from typing import TypedDict
from dataclasses import dataclass, field
# --- Course-Specific Database Models ---


@dataclass
class Meta():
    title: str
    description: str
    created_at: str


@dataclass
class Problem():
    '''Type definition for a course problem'''
    title: str
    content: str
    solved: bool = False


@dataclass
class Challenge():
    '''Type definition for a coding challenge'''
    title: str
    content: str
    solved: bool = False


@dataclass
class Project():
    '''Type definition for a course project'''
    title: str
    content: str
    start_week: int
    end_week: int
    finished: bool = False


@dataclass
class Week():
    '''Type definition for a course week'''
    theory: str
    week_number: int
    completed: bool = False
    problems: list[Problem] = field(default_factory=list)
    challenges: list[Challenge] = field(default_factory=list)


@dataclass
class Extra():
    title: str
    content: str


@dataclass
class Course():
    '''Type definition for a course'''
    __meta: Meta
    weeks: list[Week]
    projects: list[Project]
    extras: list[Extra]
    progress: float = 0

    @property
    def title(self) -> str:
        return self.__meta.title

    @title.setter
    def title(self, value: str) -> None:
        self.__meta.title = value

    @property
    def description(self) -> str:
        return self.__meta.description

    @description.setter
    def description(self, value: str) -> None:
        self.__meta.description = value

@dataclass
class CoursePreview():
    id: int
    title: str
    progress: float = 0
