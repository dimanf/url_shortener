from dto.message import ShorterUrlDto, MessageData

shorter_url_dto = ShorterUrlDto(
    url="http://test-url.com",
    data=MessageData(
        accn_id="accn_id",
        unsubscribe=False,
        msg_id="msg_id",
    ),
)
