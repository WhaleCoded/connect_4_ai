import torch


def get_and_load_model(model_path):
    model = torch.nn.Sequential(
        torch.nn.Conv2d(1, 32, kernel_size=5, padding=2),
        torch.nn.ReLU(),
        torch.nn.BatchNorm2d(32),
        torch.nn.Conv2d(32, 64, kernel_size=5, padding=2),
        torch.nn.ReLU(),
        torch.nn.BatchNorm2d(64),
        torch.nn.Conv2d(64, 128, kernel_size=5, padding=1),
        torch.nn.ReLU(),
        torch.nn.BatchNorm2d(128),
        torch.nn.Conv2d(128, 256, kernel_size=5, padding=1),
        torch.nn.ReLU(),
        torch.nn.BatchNorm2d(256),
        torch.nn.Flatten(),
        torch.nn.Linear(256 * 3 * 2, 512),
        torch.nn.LeakyReLU(),
        torch.nn.BatchNorm1d(512),
        torch.nn.Dropout(0.2),
        torch.nn.Linear(512, 128),
        torch.nn.LeakyReLU(),
        torch.nn.BatchNorm1d(128),
        torch.nn.Dropout(0.2),
        torch.nn.Linear(128, 7),
    )

    model_state_dict = torch.load(model_path)
    model.load_state_dict(model_state_dict)

    return model.eval()
