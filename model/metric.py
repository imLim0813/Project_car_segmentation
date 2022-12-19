import torch
from torch.utils.data import DataLoader
import torch.nn as nn
import torch.nn.functional as F

device_ = 'cuda:0' if torch.cuda.is_available() else 'cpu'


def pixel_accuracy(loader: DataLoader, model: nn.Module, device: str = device_) -> float:
    """
    세그멘테이션 모델 평가 함수

    :param loader: 평가 데이터셋
    :param model: 세그멘테이션 모델
    :param device: GPU 설정
    :return: Pixel accuracy, Dice score
    """
    num_correct = 0
    num_pixels = 0
    for x, y in loader:
        x = x.to(device)
        y = y.to(device)
        preds = torch.argmax(torch.softmax(model(x), dim=1), dim=1)
        num_correct += (preds == y).sum()
        num_pixels += torch.numel(preds)

    pixel_acc = (num_correct / num_pixels) * 100
    return pixel_acc.cpu().item()


def dice_score(loader: DataLoader, model: nn.Module, device: str = device_) -> float:
    """
    세그멘테이션 모델 평가 함수

    :param loader: 평가 데이터셋
    :param model: 세그멘테이션 모델
    :param device: GPU 설정
    :return: Pixel accuracy, Dice score
    """
    result = 0
    for x, y in loader:
        x = x.to(device)
        y = y.to(device)
        preds = torch.argmax(torch.softmax(model(x), dim=1), dim=1)
        result += (2 * (preds * y).sum()) / ((preds + y).sum() + 1e-8)

    result = result / len(loader)
    return result.cpu().item()
