import json
import datetime as dt
from typing import Dict, Any

from sqlmodel import SQLModel, Field, Column, Boolean, String, DateTime


class Author(SQLModel, table=True):
    name: str = Field(sa_column=Column("name", String, primary_key=True, nullable=False))
    background_color: str | None = Field(sa_column=Column("background_color", String, nullable=True))
    css_class: str | None = Field(sa_column=Column("css_class", String, nullable=True))
    richtext: str | None = Field(sa_column=Column("richtext", String, nullable=True))
    template_id: str | None = Field(sa_column=Column("template_id", String, nullable=True))
    text: str | None = Field(sa_column=Column("text", String, nullable=True))
    text_color: str | None = Field(sa_column=Column("text_color", String, nullable=True))
    type: str = Field(sa_column=Column("type", String, nullable=False))
    fullname: str = Field(sa_column=Column("fullname", String, nullable=False))
    is_blocked: bool = Field(sa_column=Column("is_blocked", Boolean, nullable=False))
    is_patreon_flair: bool = Field(sa_column=Column("is_patreon_flair", Boolean, nullable=False))
    is_premium: bool = Field(sa_column=Column("is_premium", Boolean, nullable=False))
    datetime_created: dt.datetime = Field(sa_column=Column("datetime_created", DateTime, nullable=False))
    datetime_created_utc: dt.datetime = Field(sa_column=Column("datetime_created_utc", DateTime, nullable=False))
    permalink: str = Field(sa_column=Column("permalink", String, nullable=False, unique=True))

    __tablename__ = "authors"
    __table_args__ = {"schema": "reddit"}


    class Config:
        json_schema_extra = {
            "example": {
                "name": "bluemarker23",
                "background_color": None,
                "css_class": None,
                "richtext": None,
                "template_id": None,
                "text": None,
                "text_color": None,
                "type": "text",
                "fullname": "t2_2kc53n",
                "is_blocked": False,
                "is_patreon_flair": False,
                "is_premium": False,
                "datetime_created": dt.datetime(2026, 1, 12, 0, 51, 26),
                "datetime_created_utc": dt.datetime(2026, 1, 12, 0, 51, 26),
                "url": "/r/chicagofood/comments/1qag2h9/who_is_eating_giardiniera_relish/nz2rnj7/"
            }
        }


    @staticmethod
    def from_raw_json(json_object: Dict[str, Any]) -> 'Author':
        return Author(
            name=json_object["author"],
            background_color=json_object["author_flair_background_color"] if json_object["author_flair_background_color"] else None,
            css_class=json_object["author_flair_css_class"] if json_object["author_flair_css_class"] else None,
            richtext=json.dumps(json_object["author_flair_richtext"]) if json_object["author_flair_richtext"] else None,
            template_id=json_object["author_flair_template_id"] if json_object["author_flair_template_id"] else None,
            text=json_object["author_flair_text"] if json_object["author_flair_text"] else None,
            text_color=json_object["author_flair_text_color"] if json_object["author_flair_text_color"] else None,
            type=json_object["author_flair_type"],
            fullname=json_object["author_fullname"],
            is_blocked=bool(json_object["author_is_blocked"]),
            is_patreon_flair=bool(json_object["author_patreon_flair"]),
            is_premium=bool(json_object["author_premium"]),
            datetime_created=dt.datetime.fromtimestamp(json_object['created']),
            datetime_created_utc=dt.datetime.fromtimestamp(json_object['created_utc']),
            permalink=f"/{'/'.join(json_object['url'].split('/')[3:])}",
        )