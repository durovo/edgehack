class Trainer(object):
    def __init__(self, frame_provider, human, excercise, mouth):
        self.frame_provider = frame_provider
        self.human = human
        self.excercise = excercise
        self.mouth = mouth

    def start_training(self):
        while True:
            frame = self.frame_provider.get_frame()
            self.human.update_state(frame)
            self.excercise.update_human(self.human)
            if self.excercise.next_state.has_started():
                self.excercise.transition_to_next_state()
            self.check_state_forms()
            self.check_state_direction()
    def check_state_forms(self):
        if self.excercise.state.is_motion_state:
                for form in self.excercise.state.forms:
                    is_form_correct = form.check()
                    if not is_form_correct:
                        self.mouth.speak(form.message)
    def check_state_direction(self):
        if self.excercise.state.is_motion_state:
            is_direction_correct = self.excercise.state.direction.check_direction()
            if not is_direction_correct:
                self.mouth.speak(self.excercise.state.direction.message)
