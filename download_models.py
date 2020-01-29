from itertools import chain
import os
from urllib.request import urlretrieve

from github import Github, UnknownObjectException
import npyscreen  # npyscreen.disableColor()
from progressbar import ProgressBar
from yaml import load as yaml_load


def _download_file(file_name, url):
    """Downloads a file from _url_."""
    print('Downloading ', url)
    urlretrieve(url, file_name, ReporthookProgressBar())
    print()  # Newline after download finished


def _download_github_dir(output_directory: str, repository: str,
                         git_directory: str, branch: str = 'master'):
    """
    Downloads a directory from GitHub.

    :param output_directory: the name of the output directory. If it doesn't
                             exist, it will be created.
    :param repository: the _full_ name of the GitHub repository; i.e. in the
                       {user}/{repo} format. It must be public.
    :param git_directory: the name of the directory to download.
    :param branch: the Git branch to download from.
    """
    g = Github()
    repos = g.search_repositories(repository).get_page(0)
    if not repos:
        raise ValueError(f'No such repository found: {repository}')
    if len(repos) > 1:
        raise ValueError(f'More than one repositories match to {repository}')

    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)

    dir_url = f'https://github.com/{repository}/raw/{branch}/{git_directory}'
    try:
        for git_file in repos[0].get_contents(git_directory):
            _download_file(os.path.join(output_directory, git_file.name),
                           f'{dir_url}/{git_file.name}')
    except UnknownObjectException:
        raise ValueError(f'Directory {git_directory} not found in {repository}')


def _download_selected(elems):
    """
    Downloads selected model files / directories. Model names ending with a
    slash (/) are treated as directories; otherwise, the model is assumed to be
    a single file.
    """
    for _, model_name, params in elems:
        if model_name.endswith('/'):
            _download_github_dir(model_name, **params)
        else:
            _download_file(model_name, **params)


class ReporthookProgressBar:
    """
    Original Source:
    https://stackoverflow.com/questions/37748105/how-to-use-progressbar-module-with-urlretrieve/53643011#53643011
    """
    def __init__(self):
        self.pbar = None

    def __call__(self, block_num, block_size, total_size):
        if not self.pbar:
            self.pbar = ProgressBar(maxval=total_size)
            self.pbar.start()

        downloaded = block_num * block_size
        if downloaded < total_size:
            self.pbar.update(downloaded)
        else:
            self.pbar.finish()


class MoldelSelectApp(npyscreen.NPSApp):
    def __init__(self, model_dict):
        super(MoldelSelectApp, self).__init__()
        self._models = model_dict
        self.return_value = None

    def main(self):
        main_options = [m[0] for m in self._models.get('main', [])]
        optional_options = [m[0] for m in self._models.get('optional', [])]

        form = npyscreen.Form(name='Download models')
        main_ms = form.add(npyscreen.TitleMultiSelect,
                           max_height=min(len(main_options) + 1, 8),
                           value=list(range(len(main_options))),
                           name='Main', values=main_options, scroll_exit=True)
        optional_ms = form.add(npyscreen.TitleMultiSelect,
                               max_height=min(len(optional_options) + 1, 8),
                               value=[], name='Optional',
                               values=optional_options, scroll_exit=True)
        form.edit()

        self.return_value = \
            [self._models['main'][i][0] for i in main_ms.value] + \
            [self._models['optional'][i][0] for i in optional_ms.value]


def _load_models(filename='models.yaml'):
    with open(filename, encoding='UTF-8') as fh:
        models = yaml_load(fh)
    return models


def download(available_models=None, required_models=None):
    if available_models is None:
        available_models = _load_models()
    if required_models is None:
        required_model_data = available_models
    else:
        required_model_data = [model for model in available_models
                               if model[0] in required_models]
    _download_selected(required_model_data)


if __name__ == '__main__':
    loaded_models = _load_models()
    app = MoldelSelectApp(loaded_models)
    app.run()
    ret = app.return_value
    download(list(chain.from_iterable(loaded_models.values())),
             required_models=ret)
