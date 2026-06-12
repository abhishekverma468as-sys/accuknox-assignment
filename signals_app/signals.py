import time
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyModel


# Q1 PROOF - Synchronous
execution_log = []

@receiver(post_save, sender=MyModel)
def q1_sync_proof_handler(sender, instance, created, **kwargs):
    execution_log.append(f"signal fired for: {instance.name}")


# Q2 PROOF - Same Thread
thread_log = {}

@receiver(post_save, sender=MyModel)
def q2_thread_proof_handler(sender, instance, created, **kwargs):
    thread_log['signal_thread_id'] = threading.get_ident()


# Q3 PROOF - Same Transaction
transaction_test_log = {}

@receiver(post_save, sender=MyModel)
def q3_transaction_proof_handler(sender, instance, created, **kwargs):
    transaction_test_log['handler_fired'] = True
    transaction_test_log['instance_pk'] = instance.pk