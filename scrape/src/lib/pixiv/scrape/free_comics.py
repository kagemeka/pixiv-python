import typing
import tqdm
from .free_comic import FreeComic, scrape_free_comic


def scrape_free_comics(
    comic_ids: typing.List[int],
) -> typing.Iterator[FreeComic]:
    for id_ in tqdm.tqdm(comic_ids):
        yield scrape_free_comic(id_)
