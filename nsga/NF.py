
import main
sensitive_factor = 1
def AMF_ProcessTime(current_resource):
    max_resource = 1
    min_resource = 0.2
    max_process_time = 2  # ms
    min_process_time = 0.1
    a = (max_process_time - min_process_time) / (min_resource - max_resource)
    b = (min_resource * min_process_time - max_process_time * max_resource) / (min_resource - max_resource)
    y = a * current_resource * sensitive_factor + b
    return y


def SMF_ProcessTime(current_resource):
    max_resource = 1
    min_resource = 0.2
    max_process_time = 3  # ms
    min_process_time = 0.4
    a = (max_process_time - min_process_time) / (min_resource - max_resource)
    b = (min_resource * min_process_time - max_process_time * max_resource) / (min_resource - max_resource)
    y = a * current_resource * sensitive_factor + b
    return y


def UPF_ProcessTime(current_resource):
    max_resource = 1
    min_resource = 0.2
    max_process_time = 2.5  # ms
    min_process_time = 0.2
    a = (max_process_time - min_process_time) / (min_resource - max_resource)
    b = (min_resource * min_process_time - max_process_time * max_resource) / (min_resource - max_resource)
    y = a * current_resource * sensitive_factor + b
    return y