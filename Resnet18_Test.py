import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Paths
test_path = r'Vegetables\test'

def main():
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    
    test_data = datasets.ImageFolder(test_path, transform)
    test_loader = DataLoader(test_data, batch_size=1, shuffle=False, num_workers=2)
    
    # List of class names for labels
    classes = [f'Class_{i+1}' for i in range(15)]  # Adjust according to your classes
    
    # Load saved model
    net = torch.load(r'logs\Resnet18_results\Resnet18.pt')
    net = net.cuda()
    
    y_true = []
    y_predicted = []
    correct = 0
    total = 0
    
    net.eval()  # Set model to evaluation mode
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            y_true.append(labels.item())  # Ground truth
            images, labels = images.cuda(), labels.cuda()
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            y_predicted.append(predicted.item())  # Predicted values
            
            if labels.item() == predicted.item():
                correct += 1
            total += 1
    
    accuracy = 100 * correct / total
    print(f'Accuracy of the network Resnet18: {accuracy:.2f}%')

    # Plotting accuracy as a bar chart
    plt.figure(figsize=(6, 4))
    plt.bar(['Correct Predictions', 'Incorrect Predictions'], [correct, total - correct], color=['green', 'red'])
    plt.title(f'Accuracy of the Network: {accuracy:.2f}%')
    plt.xlabel('Outcome')
    plt.ylabel('Number of Predictions')
    plt.savefig(r'logs\Resnet18_results\accuracy_bar_chart.png')  # Save the plot
    plt.show()  # Show the plot

    # Confusion Matrix
    matrix = confusion_matrix(y_true, y_predicted)
    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Labels')
    plt.ylabel('True Labels')
    plt.savefig(r'logs\Resnet18_results\confusion_matrix.png')  # Save the plot
    plt.show()  # Show the plot
    
    # Classification Report
    report_dict = classification_report(y_true, y_predicted, target_names=classes, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    plt.figure(figsize=(12, 8))
    sns.heatmap(report_df[['precision', 'recall', 'f1-score']], annot=True, cmap='coolwarm', fmt='.2f')
    plt.title('Classification Report')
    plt.xlabel('Metrics')
    plt.ylabel('Classes')
    plt.savefig(r'logs\Resnet18_results\classification_report.png')  # Save the plot
    plt.show()  # Show the plot

if __name__ == '__main__':
    torch.multiprocessing.freeze_support()  # Add this line
    main()
