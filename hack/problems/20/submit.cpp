      
#include<bits/stdc++.h>
using namespace std;

int Sum(int x){
    /* Write your code here */
    int s = 0;
while(x !=0){
int digit = x%10;
s +=digit;
x = x / 10;
}
return s;
}
int main(int argc, char const *argv[])
{
    int t;
    int x;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>x;
    result = Sum(x); 
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 

    