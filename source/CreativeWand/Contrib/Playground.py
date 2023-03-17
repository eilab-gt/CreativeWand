"""
playground.py

Just playing around XD :).
Feel free to use it as a playground for now.
"""
from StorytellingDomain.Application.Instances.Communications import GenerateComm
from StorytellingDomain.Application.Instances.Communications import ShowGeneratedComm
from StorytellingDomain.Application.Instances.Communications import UserSketchComm
from StorytellingDomain.Application.Instances.CreativeContext import StoryCreativeContext
from CreativeWand.Application.Instances.CreativeSession.StoryCreativeSession import StoryCreativeSession
from CreativeWand.Application.Instances.ExperienceManager.SimpleExperienceManager import SimpleExperienceManager

from StorytellingDomain.Application.Instances.Communications import OpeningMessageComm
from StorytellingDomain.Application.Instances.Communications import EchoComm
from StorytellingDomain.Application.Instances.Communications import InspirationComm
from StorytellingDomain.Application.Instances.Communications import UserWorkComm


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
