import sconce
import tflearn

class TflearnJob(tflearn.callbacks.Callback):
    def __init__(self, name):
        self.job = sconce.Job(name)

    def on_epoch_end(self, training_state):
        self.job.record(training_state.step, training_state.loss_value)

