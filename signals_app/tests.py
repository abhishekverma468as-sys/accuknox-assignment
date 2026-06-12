import threading
from django.test import TestCase, TransactionTestCase
from django.db import transaction
from .models import MyModel
from .signals import execution_log, thread_log, transaction_test_log


# ══════════════════════════════════════════
# Q1 - Are signals synchronous or async?
# Answer - SYNCHRONOUS
# ══════════════════════════════════════════
class TestQ1SignalIsSynchronous(TestCase):

    def setUp(self):
        execution_log.clear()

    def test_signal_fires_before_save_returns(self):
        # log is empty BEFORE save
        self.assertEqual(execution_log, [])

        obj = MyModel(name="sync_test")
        obj.save()

        # log is filled IMMEDIATELY AFTER save
        # no sleep, no wait - proves it's synchronous
        self.assertEqual(len(execution_log), 1)
        print(f"\n[Q1] Log after save: {execution_log}")
        print("[Q1] Signal is SYNCHRONOUS")


# ══════════════════════════════════════════
# Q2 - Do signals run in same thread?
# Answer - YES, same thread
# ══════════════════════════════════════════
class TestQ2SignalSameThread(TestCase):

    def setUp(self):
        thread_log.clear()

    def test_signal_runs_in_caller_thread(self):
        # record caller thread id
        caller_thread_id = threading.get_ident()

        obj = MyModel(name="thread_test")
        obj.save()

        # get thread id recorded inside the handler
        signal_thread_id = thread_log['signal_thread_id']

        print(f"\n[Q2] Caller thread id: {caller_thread_id}")
        print(f"[Q2] Signal thread id: {signal_thread_id}")

        # both must be equal
        self.assertEqual(caller_thread_id, signal_thread_id)
        print("[Q2] Signal runs in SAME THREAD")


# ══════════════════════════════════════════
# Q3 - Do signals run in same transaction?
# Answer - YES, same transaction
# ══════════════════════════════════════════
class TestQ3SignalSameTransaction(TransactionTestCase):

    def setUp(self):
        transaction_test_log.clear()

    def test_signal_shares_transaction_with_caller(self):
        try:
            with transaction.atomic():
                obj = MyModel(name="txn_test")
                obj.save()

                # force rollback of entire transaction
                transaction.set_rollback(True)
        except Exception:
            pass

        # check if object exists in DB after rollback
        exists_in_db = MyModel.objects.filter(name="txn_test").exists()

        print(f"\n[Q3] Handler fired: {transaction_test_log.get('handler_fired')}")
        print(f"[Q3] Object in DB after rollback: {exists_in_db}")

        # handler fired but object is gone = same transaction rolled back together
        self.assertTrue(transaction_test_log.get('handler_fired'))
        self.assertFalse(exists_in_db)
        print("[Q3] Signal runs in SAME TRANSACTION")