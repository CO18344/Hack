      
#include<bits/stdc++.h>
using namespace std;

int array_maxima(int arr[],int n){
    /* Write your code here */
   int max = arr[0];
   for(int i=0;i<n;i++){
    if(arr[i] > max)
    max = arr[i];
}

return max;

}
int main(int argc, char const *argv[])
{
    int t;
    int n;
    int *arr;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>n;
    arr = new int[n];
    for(int j = 0;j<n;j++)
        cin>>arr[j];
    result = array_maxima(arr,n); 
    cout<<result<<endl;
    delete[] arr;
    }
 	
 	
 	return 0;
} 

    