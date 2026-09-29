from client import CheckpointSerializer

ckpt = CheckpointSerializer()
c1 = ckpt.commit_checkpoint("step1", {"status": "ok"})
print("Committed checkpoint:", c1["checkpoint_id"])
print("Restored state:", ckpt.restore_checkpoint(c1["checkpoint_id"]))
