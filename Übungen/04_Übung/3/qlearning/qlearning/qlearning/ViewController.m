//
//  ViewController.m
//  qlearning
//
//  Created by Julia Kindelsberger on 13/06/16.
//  Copyright © 2016 Julia Kindelsberger. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()
@property (weak, nonatomic) IBOutlet UIButton *goodButton;

@property (weak, nonatomic) IBOutlet UILabel *label;
@property (weak, nonatomic) IBOutlet UIButton *badButton;
@property (weak, nonatomic) IBOutlet UILabel *pointsLabel;
@property (weak, nonatomic) IBOutlet UIImageView *image;

@end

NSArray *imageArray;
NSMutableArray *qmatrix;

const double alpha = 0.5;
const double gam = 0.5;
int currentImageIndex = 0;


bool liked;

@implementation ViewController
- (IBAction)goodButtonAction:(id)sender {
    self.label.text = @"button one clicked";
    liked = true;
    
    [self chooseAction];
}
- (IBAction)badButtonAction:(id)sender {
    self.label.text = @"bad two clicked";
    liked = false;
    [self chooseAction];
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
    
    imageArray = [NSArray arrayWithObjects:
                   [UIImage imageNamed:@"crop.jpeg"],
                   [UIImage imageNamed:@"beach.jpg"],
                  [UIImage imageNamed:@"rain-2.jpg"],
                  [UIImage imageNamed:@"rain.jpg"],
                   nil];
    
    qmatrix = [[NSMutableArray alloc] init];
    NSNumber *num = [NSNumber numberWithFloat:0.0];
    [qmatrix addObject:num];
    NSNumber *num2 = [NSNumber numberWithFloat:0.0];
    [qmatrix addObject:num2];
    NSNumber *num3 = [NSNumber numberWithFloat:0.0];
    [qmatrix addObject:num3];
    NSNumber *num4 = [NSNumber numberWithFloat:0.0];
    [qmatrix addObject:num4];
    
    currentImageIndex = arc4random_uniform(4);
    self.image.image = imageArray[currentImageIndex];
    self.label.text = [NSString stringWithFormat:@"%@ %i", @"Nr: " , currentImageIndex];
    
    [self.goodButton setTitleColor:[UIColor greenColor] forState:UIControlStateNormal];
    [self.badButton setTitleColor:[UIColor redColor] forState:UIControlStateNormal];
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (void)chooseAction {
    
    
    float zero = [[qmatrix objectAtIndex:0] floatValue];
    float one = [[qmatrix objectAtIndex:1 ] floatValue];
    float two = [[qmatrix objectAtIndex:2] floatValue];
    float three = [[qmatrix objectAtIndex:3 ] floatValue];

    
    
    NSNumber *max=[qmatrix valueForKeyPath:@"@max.doubleValue"];
    double maxDouble = [max doubleValue];
    
    double reward = 0;
    
    if (liked) {
        reward = 100;
    } else {
        reward = -100;
    }
    
    double qValue = [[qmatrix objectAtIndex: currentImageIndex]doubleValue];
    double q = qValue + alpha * (reward + maxDouble * gam - qValue);
    
    
    [qmatrix replaceObjectAtIndex:currentImageIndex withObject:[NSNumber numberWithDouble:q]];
    
    NSUInteger random = arc4random_uniform(11);

    if (random <= 2) {
        NSLog(@"random <=2 currentImageIndex");
    
        currentImageIndex = arc4random_uniform(4);
 
        NSLog(@"%i",currentImageIndex);
        
    } else if(3 <= random && random <= 10){
                NSLog(@"random between");
        
        max=[qmatrix valueForKeyPath:@"@max.doubleValue"];
        NSInteger maxQIndex=[qmatrix indexOfObject: max];
        currentImageIndex = maxQIndex;

        NSLog(@"%i",currentImageIndex);
    } else {
         NSLog(@"choose second highest");
        
     
        NSMutableArray *newArray = [[NSMutableArray alloc] initWithArray:qmatrix copyItems:YES];
        max=[newArray valueForKeyPath:@"@max.doubleValue"];
        [newArray delete:max];
        NSNumber *secondHighest = [newArray valueForKeyPath:@"@max.doubleValue"];
        NSInteger maxQIndex=[qmatrix indexOfObject: secondHighest];
        currentImageIndex = maxQIndex;
        
       }
    
    NSLog(@"-------------");
 
        self.image.image = imageArray[currentImageIndex];
        self.label.text = [NSString stringWithFormat:@"%@ %i", @"Nr: " , currentImageIndex];
    
    NSLog(@"%f %f %f %f", zero, one, two, three);
    self.pointsLabel.text = [NSString stringWithFormat:@"%.02f %@ %.02f %@ %.02f %@  %.02f", zero, @" ", one, @" ", two, @" ", three];

    
}

@end
