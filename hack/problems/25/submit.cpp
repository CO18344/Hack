      
#include<bits/stdc++.h>
using namespace std;

void Swap(int &a, int &b){
    /* Write your code here */
int temp = a;
a = b;
b = temp;

}
int main(int argc, char const *argv[])
{
    int t;
    int a;
    int b;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>a>>b;
    Swap(a,b);
    cout<<a<<" "<<b<<endl;
    }
 	
 	
 	return 0;
} 

    