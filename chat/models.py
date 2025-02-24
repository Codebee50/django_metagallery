from django.db import models
from accounts.models import UserAccount
from django.db.models import Q

class ThreadManager(models.Manager):
    def by_user(self, user):
        """
        Get all threads related to a user account
        """
        
        lookup_one = Q(user_one=user) | Q(user_two=user)
        lookup_two = Q(user_one=user) & Q(user_two=user)#A user cannot have a thread with himself

        qs = self.get_queryset().filter(lookup_one).exclude(lookup_two)
        return qs
    
    def get_thread(self, user_one_id, user_two_id):
        if user_one_id == user_two_id:
            return None
        
        qLookup_one = Q(user_one__id=user_one_id) & Q(user_two__id = user_two_id)
        qLookup_two = Q(user_one__id=user_two_id) & Q(user_two__id=user_one_id)

        query_set = self.get_queryset().filter(qLookup_one | qLookup_two)
        return query_set
    
    def get_or_new(self, user, other_user_id):
        """
        gets or creates a new thread related to User user and user with an id of other_userId
        returns Thread (created or found thread object), Boolean(true if a new thread was created, false otherwise)
        """
        user_id = user.id
        if user_id == other_user_id:
            return None, False
        
        qlookup_one = Q(user_one__id=user_id) & Q(user_two__id=other_user_id)
        qlookup_two = Q(user_one__id=other_user_id) & Q(user_two__id=user_id)
        
        query_set = self.get_queryset().filter(qlookup_one | qlookup_two).distinct()
        
        if query_set.count() == 1:
            return query_set.first(), False
        elif query_set.count() > 1:
            return query_set.order_by('created').first(), False
        else:
            try:
                other_user = UserAccount.objects.get(id=other_user_id)
            except UserAccount.DoesNotExist:
                return None, False

            if user != other_user:
                obj = self.model(
                    user_one = user,
                    user_two = other_user
                )

                obj.save()
                return obj, True
            return None, False


class ChatManager(models.Manager):
    def create_chat(self, sender, receiverId, message, thread, commit=True):
        if sender.id == receiverId:
            return None, 'Sender and receiver cannot be the same'
        
        try:
            receiver = UserAccount.objects.get(id=receiverId)
            obj = self.model(
                thread=thread,
                sender=sender,
                receiver = receiver,
                message=message
            )

            if commit:
                obj.save()
            return obj, 'Chat created'
        except:
            return None, 'Receiver was not found'


class Thread(models.Model):
    user_one = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='thread_user_one')
    user_two = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='thread_user_two')
    
    objects = models.Manager()
    threadm = ThreadManager()
    
    def __str__(self):
        return f"{self.user_one.email} -> {self.user_two.email}"
    
class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="msgs_sent")
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name="msgs_received")
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    objects = models.Manager()
    chatm = ChatManager()
    
    class Meta: 
        ordering = ['-created']
        indexes = [
            models.Index(fields=['sender', 'receiver']),
            models.Index(fields=['-created'])
        ]