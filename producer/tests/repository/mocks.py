from dto.message import ShorterUrlCreate, MessageData

shorter_url_create = ShorterUrlCreate(
    msg_id="msg_id",
    original_url="original_url",
    short_url="short_url",
    data=MessageData(
        accn_id="accn_id",
        unsubscribe=False,
        msg_id="msg_id",
    ),
)
