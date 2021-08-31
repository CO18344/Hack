      
#include<bits/stdc++.h>
using namespace std;

int palindrome(int x){
    /* Write your code here */
   int rev = 0;
   int num = x;

  while(x != 0){
   int digit = x  % 10;
  rev = rev * 10 + digit;
  x = x / 10;
}

return num == rev;

}
int main(int argc, char const *argv[])
{
    int t;
    int x;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>x;
    result = palindrome(x);
    cout<<result<<endl;
    }
 	
 	
 	return 0;
} 

    