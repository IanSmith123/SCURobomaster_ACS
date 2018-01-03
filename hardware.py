from evdev import InputDevice, ecodes  # only some linux(ubuntu,debian...) has this package
from typing import Sequence
import threading
import utils
import dao

# singleton
DEFAULT_CARD_INPUT_DEVICE = '/dev/input/by-id/usb-HXGCoLtd_HIDKeys-event-kbd'

__current_card_id = ""
__inside_visitors_dic = {}  # card_id ---> enter_time
__dev = None
__importing_mode = False
__mode_lock = threading.Lock()
__update_time = utils.get_current_time()


def start(device=DEFAULT_CARD_INPUT_DEVICE):
    global __dev
    # init device
    if __dev is None:
        __dev = InputDevice(device)
        input_thread = threading.Thread(target=__working_loop, name='input-listen')
        input_thread.start()
        print("Hardware started")


def get_current_card_id() -> str:
    return __current_card_id


def get_inside_visitors_card_id() -> Sequence[str]:
    return [k for k in __inside_visitors_dic]


def set_importing_mode():
    global __importing_mode
    __mode_lock.acquire()
    __importing_mode = True
    __mode_lock.release()


def get_update_time():
    return __update_time


def __working_loop():
    global __current_card_id, __importing_mode, __update_time
    last_value = 28
    last_key = None
    card_id = ""
    for event in __dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key = 28 if event.code == 28 else (event.code - 1) % 10
            if key != last_key:
                last_key = key
                last_value = event.value
            else:
                if last_value == 1 and event.value == 0:
                    if key == 28:  # enter pressed
                        print("ACCESS:" + card_id)
                        curr_time = utils.get_current_time()
                        __mode_lock.acquire()
                        # persist
                        __persist_raw_record(card_id, curr_time)
                        if card_id in __inside_visitors_dic:
                            enter_time = __inside_visitors_dic.pop(card_id)
                            __persist_access_record(card_id, enter_time, leave_time=curr_time)
                        else:
                            __inside_visitors_dic[card_id] = curr_time
                        if __importing_mode:
                            __importing_mode = False
                        __mode_lock.release()
                        __current_card_id = card_id
                        __update_time = curr_time  # I'm not sure if this operation is atomic and thread-safe :)
                        card_id = ""
                    else:
                        card_id += str(key)
                last_value = event.value


def __persist_raw_record(card_id, time):
    if __importing_mode:
        return
    try:
        dao.persist_raw_record(card_id, time)
    except Exception as e:
        print("error", str(utils.get_current_time()), str(e))
        pass


def __persist_access_record(card_id, enter_time, leave_time):
    if __importing_mode:
        return
    try:
        dao.persist_access_record(card_id, enter_time, leave_time)
    except Exception as e:
        print("error", str(utils.get_current_time()), str(e))
