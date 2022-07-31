"""
playground.py

Just playing around XD :).
Feel free to use it as a playground for now.
"""
from CreativeWand.Application.Instances.Communications.StoryContext.RequestGeneration import GenerateComm
from CreativeWand.Application.Instances.Communications.StoryContext.ShowGenerated import ShowGeneratedComm
from CreativeWand.Application.Instances.Communications.StoryContext.UserProvideSketch import UserSketchComm
from CreativeWand.Application.Instances.CreativeContext.StoryCreativeContext import StoryCreativeContext
from CreativeWand.Application.Instances.CreativeSession.StoryCreativeSession import StoryCreativeSession
from CreativeWand.Application.Instances.ExperienceManager.SimpleExperienceManager import SimpleExperienceManager

from CreativeWand.Application.Instances.Communications.OpeningMessage import OpeningMessageComm
from CreativeWand.Application.Instances.Communications.Echo import EchoComm
from CreativeWand.Application.Instances.Communications.StoryContext.InspirationComm import InspirationComm
from CreativeWand.Application.Instances.Communications.StoryContext.UserWorkComm import UserWorkComm


def test_simple_em():
    """
    Test SimpleExperienceManager.
    :return:
    """

    sem = SimpleExperienceManager()
    sem.bind_creative_context(StoryCreativeContext())

    sem.register_communication(OpeningMessageComm())
    sem.register_communication(EchoComm())
    sem.register_communication(UserSketchComm())
    sem.register_communication(ShowGeneratedComm())
    sem.register_communication(GenerateComm())
    sem.register_communication(UserWorkComm())
    sem.register_communication(InspirationComm())

    sess = StoryCreativeSession(manager=sem)

    sess.start_session()


if __name__ == '__main__':
    test_simple_em()
