import enum

class GenderEnum(str, enum.Enum):
    female = "женский"
    male = "мужской"

class VkActionEnum(str, enum.Enum):
    like = "like"
    comment = "comment"
    post = "post"

class TgActionEnum(str, enum.Enum):
    tag = "tag"
    react = "react"
    message = "message"
    add_user = "add_user"
    reply = "reply"
    delete = "delete"
    forward = "forward"

class FamilyStatusEnum(str, enum.Enum):
  not_selected = "не выбрано"
  single_female = "не замужем"
  single_male = "не женат"
  has_boyfriend = "есть друг"
  has_girlfriend = "есть подруга"
  engaged_female = "помолвлена"
  engaged_male = "помолвлен"
  married_female = "замужем"
  married_male = "женат"
  in_love_female = "влюблена"
  in_love_male = "влюблен"
  active_search = "в активном поиске"
  civil_marriage = "в гражданском браке"