class Checker(object):
    def __init__(self, message_time_gap, reset_time_gap, checker, message):
        self.check_pass = True
        self.message = message
        self.time = 0
        self.display_message = False
        self.checker = checker
        self.reset_time = 0
        self.message_time_gap = message_time_gap
        self.reset_time_gap = reset_time_gap
    def check(self, wes, esh, shk, seh, sek):
        if self.checker(wes, esh, shk, seh, sek):
            self.check_pass = False
            self.reset_time = 0
            print(self.message)
            print(self.time)
            if self.time == 0:
                self.time = time.time()

                self.display_message = True
            else:
                d = time.time() - self.time
                if d > self.message_time_gap:
                    self.display_message = True
                    self.time = 0
                else:
                    self.display_message = False                
        else:
            self.reset()
        return self.check_pass
    def reset(self):
        if self.reset_time == 0:
            self.reset_time = time.time()
        else:
            if time.time() - self.reset_time > self.reset_time_gap:

                print("Resetting")
                self.check_pass = True
                self.display_message = False
                self.time = 0
                self.reset_time = 0