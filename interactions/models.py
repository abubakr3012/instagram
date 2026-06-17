from django.db import models
from django.contrib.auth import get_user_model
from videos.models import Videos

User = get_user_model()


class Comment(models.Model):
    video = models.ForeignKey(Videos, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent_comment = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )
    comment_text = models.TextField()
    photo = models.ImageField(upload_to="comments/", blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} → {self.comment_text[:50]} on '{self.video.title}'"

    @property
    def is_reply(self):
        return self.parent_comment_id is not None

    def get_reply_count(self):
        return self.replies.filter(is_deleted=False).count()


class Like(models.Model):
    video = models.ForeignKey(
        Videos, on_delete=models.CASCADE,
        null=True, blank=True, related_name="likes"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE,
        null=True, blank=True, related_name="likes"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "video"],
                condition=models.Q(video__isnull=False),
                name="unique_video_like",
            ),
            models.UniqueConstraint(
                fields=["user", "comment"],
                condition=models.Q(comment__isnull=False),
                name="unique_comment_like",
            ),
        ]

    def __str__(self):
        target = self.video or self.comment
        return f"{self.user.username} лайкнул {target}"