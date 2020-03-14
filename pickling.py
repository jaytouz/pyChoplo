import pickle


def create_pickle(data_name, data):
    """data_name without the .pickle"""
    file_name = '{}.pickle'.format(data_name)
    with open(file_name, 'wb') as handle:
        pickle.dump(data, handle)
    print('done, {} , pickle saved'.format(data_name))


def load_pickle(data_name):
    file_name = '{}.pickle'.format(str(data_name))
    with open(file_name, 'rb') as handle:
        data = pickle.load(handle)
    return data
