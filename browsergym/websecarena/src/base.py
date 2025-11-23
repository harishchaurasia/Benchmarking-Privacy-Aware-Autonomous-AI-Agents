from browsergym.core.task import AbstractBrowserTask
from pyparsing import Optional
import os


class AbstractWebSecArenaTask(AbstractBrowserTask):
    """
    Abstract class for all WebSecArena tasks

    """

    @classmethod
    def get_task_id(cls):
        return f"websecarena.{cls.subdomain}"

    def __init__(
        self,
        seed: int,
        base_url: Optional = None,
        episode_max_time: int = 1000000,
        remove_human_display: bool = True,
    ) -> None:
        """
        Args:
            seed: random seed.
            base_url: str (optional), the base WebSecArena URL where the task's HTML file is to be found. If not provided, the WEB_SEC_ARENA_URL environment variable will be used.
            episode_max_time: int, episode max time in milliseconds. Default: 1000000 ms.
            remove_human_display: bool, whether or not to remove the human display (goal, time left, last reward etc.) from the DOM. Default: True.

        """
        super().__init__(seed)

        # Screenshot is scaled for this banchmark see `_bgym_scale_factor`
        # Keeping this aspect ratio and size works well with claude-3.5 so far.
        # But may not be optimal for other VLMs.
        self.viewport = {"width": 332, "height": 214}
        self.slow_mo = 100  # ms
        self.timeout = 5000  # ms

        assert episode_max_time > 0

        # if not provided, try to get WebSecArena URL from environment variable
        if base_url is None:
            if "WEB_SEC_ARENA_URL" in os.environ:
                base_url = os.environ["WEB_SEC_ARENA_URL"]
                self.url = base_url + self.subdomain + ".html"
            else:
                self.url = None

        self.episode_max_time = episode_max_time
        self.remove_human_display = remove_human_display