import enum

class VkActionEnum(str, enum.Enum):
    like = "like"
    comment = "comment"

class TgActionEnum(str, enum.Enum):
    tag = "tag"
    react = "react"
    message = "message"
    add_user = "add_user"