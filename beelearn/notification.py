from functools import partial
import json
from typing import List, Literal, Optional

from firebase_admin.messaging import Message as FcmMessage, Notification


ChannelKey = Literal[
    "comment_channel",
    "general_channel",
    "in_app_channel",
]
NotificationLayout = Literal[
    "Default",
    "Inbox",
    "Messaging",
    "BigPicture",
    "Messaging",
    "MessagingGroup",
]

ActionType = Literal[
    "Default",
    "SilentAction",
    "SilentBackgroundAction",
    "KeepOnTop",
    "DisabledAction",
    "DismissAction",
]


class PushNotification(Notification):
    pass


class MessageAction(dict):
    def __init__(
        self,
        key: str,
        label: str,
        autoDismissible: bool = False,
        requireInputText: bool = False,
        actionType: ActionType = "Default",
        isDangerousOption: bool = False,
    ):
        dict.__init__(
            self,
            key=key,
            label=label,
            actionType=actionType,
            autoDismissible=autoDismissible,
            requireInputText=requireInputText,
            isDangerousOption=isDangerousOption,
        )


class MessageContent(dict):
    def __init__(
        self,
        showWhen: bool = True,
        badge: Optional[int] = None,
        privacy: Optional[str] = None,
        payload: Optional[dict] = None,
        largeIcon: Optional[str] = None,
        bigPicture: Optional[str] = None,
        displayOnForeground: bool = True,
        channelKey: ChannelKey = "general_channel",
        notificationLayout: NotificationLayout = "Default",
    ):
        dict.__init__(
            self,
            badge=badge,
            payload=payload,
            privacy=privacy,
            showWhen=showWhen,
            largeIcon=largeIcon,
            bigPicture=bigPicture,
            channelKey=channelKey,
            notificationLayout=notificationLayout,
            displayOnForeground=displayOnForeground,
        )


def Message(
    token: str,
    content: MessageContent,
    actions: List[MessageAction],
    notification: PushNotification,
):
    assert isinstance(actions, (list, tuple)), "actions must be an iterable"

    return FcmMessage(
        token=token,
        notification=notification,
        data={
            "content": json.dumps(content),
            "actionButtons": json.dumps(actions),
        },
    )


def build_inbox_message(
    token: str,
    title: str,
    body: str,
    avatar: str,
    payload: dict,
    channelKey: ChannelKey = "comment_channel",
):
    return Message(
        token=token,
        notification=PushNotification(
            title=title,
            body=body,
        ),
        content=MessageContent(
            payload=payload,
            largeIcon=avatar,
            channelKey=channelKey,
            notificationLayout="Inbox",
        ),
        actions=[
            MessageAction(
                key="DISMISS",
                label="Dismiss",
                autoDismissible=True,
                isDangerousOption=True,
            ),
            MessageAction(
                key="REPLY",
                label="Reply",
                requireInputText=True,
            ),
        ],
    )
