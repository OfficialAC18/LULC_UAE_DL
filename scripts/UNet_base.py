import torch 
import torch.nn as nn


class DualConv(nn.Module):
        def __init__(self, in_channels, out_channels) -> None: 
            super(DualConv, self).__init__()
            self.conv = nn.Sequential(
                  nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1, bias=False),
                  nn.BatchNorm2d(out_channels),
                  nn.ReLU(inplace=True),
                  nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1, padding=1, bias=False),
                  nn.BatchNorm2d(out_channels),
                  nn.ReLU(inplace=True)
            )

        def forward(self,x):
              return self.conv(x)
        

class UNet(nn.Module):
      def __init__(self,
                   in_channels,
                   out_channels,
                   img_height = 1024,
                   img_width = 1024,
                   n_classes = 8,
                   features = [64, 128, 256, 512]) -> None:
            
            super(UNet, self).__init__()
            self.downs = nn.ModuleList()
            self.ups = nn.ModuleList()
            self.pool = nn.MaxPool2d(kernel_size=2, stride=2)


            #Encoding Part of UNet
            for feature in features:
                self.downs.append(DualConv(in_channels=in_channels,out_channels = feature))
                
                #Updating the in_channels parameter
                in_channels = feature
            
            #Decoding Part of UNet
            for feature in reversed(features):
                  self.ups.append(nn.ConvTranspose2d(
                        feature*2,feature, kernel_size=2, stride=2 
                  ))


            
