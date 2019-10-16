import os
from urllib.request import urlretrieve

import npyscreen  # npyscreen.disableColor()
from progressbar import ProgressBar
from yaml import load as yaml_load


def _download_selected(elems):
    for _, file_name, url in elems:
        out_file_name = os.path.join(os.path.dirname(__file__), file_name)
        print('Downloading ', url)
        urlretrieve(url, out_file_name, ReporthookProgressBar())
        print()  # Newline after download finished


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
    def __init__(self, model_list):
        super(MoldelSelectApp, self).__init__()
        self._models = model_list
        self.return_value = None

    def main(self):
        options = [m[0] for m in self._models]

        form = npyscreen.Form(name='Download models')
        ms2 = form.add(npyscreen.TitleMultiSelect, value=list(range(len(options))), name='Models to download',
                       values=options)
        form.edit()

        self.return_value = [self._models[i][0] for i in ms2.value]


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
        required_model_data = [model for model in available_models if model[0] in required_models]
    _download_selected(required_model_data)


if __name__ == '__main__':
    loaded_models = _load_models()
    app = MoldelSelectApp(loaded_models)
    app.run()
    ret = app.return_value
    download(loaded_models, required_models=ret)
