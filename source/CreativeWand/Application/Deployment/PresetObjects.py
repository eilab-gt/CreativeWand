"""
PresetObjects.py

Some pre-built objects (experience manager with communications filled in, etc.) useful for other files.

"""

# region Register Presets
# todo: make all these dynamic
import CreativeWand.Application.Deployment.Presets.StoryPresets as sp

comm_presets_functions = {
    "story": sp.create_comms_from_preset,
}

domain_specific_types = {
    "story": sp.class_name_to_type,
}


# endregion

def create_session(
        experience_manager_class_name: str = "ExperienceManager",
        frontend_class_name: str = "Frontend",
        creative_context_class_name: str = "CreativeContext",
        frontend_args=None,
        creative_context_args=None,
        domain: str = None,
        presets: str = None,
        em_info: dict = None):
    """
    Creates a new experienceManager object with specified paramters.
    This function first translate names into their corresponding classes.
    :param experience_manager_class_name: name of the experience manager class.
    :param frontend_class_name: name of the frontend.
    :param creative_context_class_name: name of the creative context.
    :param frontend_args: arguments to pass to the frontend __init__().
    :param creative_context_args: arguments to pass to the CreativeContext __init__().
    :param domain: domain of this setup, used to find communications.
    :param presets: preset name for communications, used to find communications.
    :param em_info: passed as `info` argument to the experiment manager __init__().
    :return: The experience manager.
    """
    emc = domain_specific_types[domain][experience_manager_class_name]
    fc = domain_specific_types[domain][frontend_class_name]
    ccc = domain_specific_types[domain][creative_context_class_name]

    return create_session_helper(
        experience_manager_class=emc, frontend_class=fc, creative_context_class=ccc,
        frontend_args=frontend_args,
        creative_context_args=creative_context_args,
        domain=domain,
        presets=presets,
        em_info=em_info
    )


def create_session_helper(
        experience_manager_class: type,
        frontend_class: type,
        creative_context_class: type,
        frontend_args=None,
        creative_context_args=None,
        domain: str = None,
        presets: str = None,
        em_info: dict = None):
    """
    Creates a new experienceManager object with specified paramters.
    :param experience_manager_class: class type of the experience manager.
    :param frontend_class: class type of the frontend.
    :param creative_context_class: class type of the creative context.
    :param frontend_args: arguments to pass to the frontend __init__().
    :param creative_context_args: arguments to pass to the CreativeContext __init__().
    :param domain: domain of this setup, used to find communications.
    :param presets: preset name for communications, used to find communications.
    :param em_info: passed as `info` argument to the experiment manager __init__().
    :return: The experience manager.
    """
    if creative_context_args is None:
        creative_context_args = {}
    if frontend_args is None:
        frontend_args = {}
    sem = experience_manager_class(frontend=frontend_class(**frontend_args), info=em_info)
    sem.bind_creative_context(creative_context_class(**creative_context_args))
    comms = comm_presets_functions[domain](name=presets)
    for item in comms:
        sem.register_communication(item)
    return sem
