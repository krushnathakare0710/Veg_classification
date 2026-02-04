import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.autograd import Variable
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import torchvision.models as models
from torchvision.models import ResNet18_Weights



# Paths 
train_path = r"Vegetables\train"
test_path =  r"Vegetables\test"
validation_path= r"Vegetables\validation"


def main():
# TRANSFORM
    transform =transforms.Compose([
               #transforms.RandomHorizontalFlip(),
		       transforms.Resize((224,224)),
          
		       #transforms.ColorJitter(brightness=0.1,constrast=0.1,saturation=0.1,hue=0.1),
		       transforms.ToTensor(),
		       #transforms.Normalize(mean = [ 0.7953, 0.4296, 0.9194 ],
				           # std = [ 1.00000e-02 *
                           #        9.4772, 0.1594, 1.00000e-02 *
                        #       2.5133 ]),
                              ])
                        
    # Loading data from a image folder
    train_data = datasets.ImageFolder(train_path ,transform)

    validation_data = datasets.ImageFolder(validation_path , transform)
    
    # Loading data in batches                                       
    train_loader = DataLoader(train_data, batch_size=32, shuffle=True, num_workers=4, pin_memory=True)
    validation_loader = DataLoader(validation_data , batch_size=8, shuffle=True, num_workers=4, pin_memory=True)
    
    
    # net= models.resnet18(pretrained=True)
    net= models.resnet18(weights=ResNet18_Weights.DEFAULT)
    net.fc=nn.Linear(in_features=512,out_features=15);
    
    # Transfering network to GPU RAM 
    net = net.cuda();       
    
    # Define the loss Function
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(),lr=0.0001)
    train_loss_vs_epoch=[]
    validation_loss_vs_epoch=[]

    print("Training Started...")
    # Training the network 
    min_validation = 9999
    for epoch in range(15) :  # epochs : loop over the dataset multiple times
        train_loss = 0.0
        # Training
        for i,batch in enumerate(train_loader,0):
            net=net.train(True) # Training Mode
            # get the inputs
            inputs, labels = batch
            inputs, labels = inputs.cuda(), labels.cuda()
            # wrap them in Variable for autograd
            inputs, labels = Variable(inputs), Variable(labels) 
                
            # zero the parameter gradients
            optimizer.zero_grad()
            # forward + backward + optimize
            outputs = net(inputs)
            loss = criterion(outputs, labels)
           
            loss.backward()
            optimizer.step()
    
            train_loss += loss.item()
        train_loss_vs_epoch.append(train_loss/len(train_loader))
        
        validation_loss = 0.0
        for batch in validation_loader :
            net = net.train(False)
            inputs, labels = batch
           # inputs, labels = Variable(inputs), Variable(labels) 
            inputs, labels = inputs.cuda(),labels.cuda();
            inputs, labels = Variable(inputs), Variable(labels) 
            outputs = net(inputs)
            loss = criterion(outputs, labels)        
            validation_loss += loss.item()
       
        validation_loss_vs_epoch.append(validation_loss/len(validation_loader))  
         
         
        plt.plot(train_loss_vs_epoch,'r',validation_loss_vs_epoch,'b')
        plt.savefig(r'logs\Resnet18_results\plot_resnet18.png')
        
        if validation_loss < min_validation :
            min_validation = validation_loss
            torch.save(net, r"logs\Resnet18_results\Resnet18.pt");
            print('model saved')
        # Total Loss each epoch
        print('[epoch: %d] train loss: %.6f, val loss= %0.6f' %(epoch+1, train_loss/len(train_loader), validation_loss/len(validation_loader)))
        
    print('Finished Training')

    # plt.plot(train_loss_vs_epoch,'r',validation_loss_vs_epoch,'b')
    # plt.xlabel('No. of epoch')
    # plt.ylabel('Loss per epoch')
    # plt.title('Resnet18')
    # plt.savefig('plot_Resnet18.png')

if __name__ == '__main__':
    torch.multiprocessing.freeze_support()  # Add this line
    main()

 