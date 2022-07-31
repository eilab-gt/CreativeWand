"""
main.py

Entry point for system testing.
Feel free to use it as a playground for now.
"""

from CreativeWand.Application.Instances.Communications.StoryContext.RequestGeneration import GenerateComm, \
    GenerateWithFreezeComm
from CreativeWand.Application.Instances.Communications.StoryContext.ShowGenerated import ShowGeneratedComm
from CreativeWand.Application.Instances.Communications.StoryContext.UserProvideSketch import UserSketchComm
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryCreativeContext
from CreativeWand.Application.Instances.ExperienceManager.SimpleExperienceManager import SimpleExperienceManager
from CreativeWand.Application.Instances.CreativeSession.StoryCreativeSession import StoryCreativeSession

from CreativeWand.Application.Instances.Communications.OpeningMessage import OpeningMessageComm
from CreativeWand.Application.Instances.Communications.Echo import EchoComm
from CreativeWand.Application.Instances.Communications.StoryContext.InspirationComm import InspirationComm
from CreativeWand.Application.Instances.Communications.StoryContext.UserWorkComm import UserWorkComm
from CreativeWand.Application.Instances.Communications.StoryContext.TopicRegenerationComm import TopicRegenerationComm
from CreativeWand.Application.Instances.Communications.StoryContext.SuggestSentenceComm import SuggestSentenceComm
from CreativeWand.Application.Instances.Frontend.WebFrontendHelper.WebFrontendServer import run_server


def test_simple_em():
    """
    Test SimpleExperienceManager.
    :return:
    """

    # We can specify frontend here.
    # sem = SimpleExperienceManager(frontend=CommandLineFrontend())
    sem = SimpleExperienceManager()
    sem.bind_creative_context(StoryCreativeContext())

    sem.register_communication(OpeningMessageComm())
    sem.register_communication(EchoComm())
    sem.register_communication(UserSketchComm())
    sem.register_communication(ShowGeneratedComm())
    sem.register_communication(GenerateComm())
    sem.register_communication(GenerateWithFreezeComm())
    sem.register_communication(UserWorkComm())
    sem.register_communication(InspirationComm())
    sem.register_communication(TopicRegenerationComm())
    sem.register_communication(SuggestSentenceComm())

    sess = StoryCreativeSession(manager=sem)

    sess.start_session()


if __name__ == '__main__':
    # test_simple_em()

    run_server(run_async=True)
