      
#include<bits/stdc++.h>
using namespace std;

int leap(int x){
    /* Write your code here */
int year = x;
if (year % 4 == 0) {
        if (year % 100 == 0) {
            if (year % 400 == 0)
                return 1;
            else
                return 0;
        }
        else
             return 1;
    }
    else
        return 0;

}
int main(int argc, char const *argv[])
{
    int t;
    int x;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>x;
    result = leap(x);
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 

    