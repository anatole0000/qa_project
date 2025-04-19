from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Question(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', default=1)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current timestamp when created

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(default='No content provided')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', default=1)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current timestamp when created

    def __str__(self):
        return f"Answer to: {self.question.title} by {self.user.username}"
    
    def vote_count(self):
        return self.votes.aggregate(score=models.Sum('value'))['score'] or 0

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='votes')
    value = models.IntegerField(choices=[(1, 'Upvote'), (-1, 'Downvote')])  # +1 for upvote, -1 for downvote
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set to the current timestamp when created

    class Meta:
        unique_together = ('user', 'answer')  # Prevent duplicate votes
