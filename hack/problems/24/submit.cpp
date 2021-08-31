      
#include<bits/stdc++.h>
using namespace std;

void Sort(int arr[], int n){
    /* Write your code here */
   sort(arr,arr+n);

}
int main(int argc, char const *argv[])
{
    int t;
    int n;
    int *arr = 0;
    int result;
    cin>>t;

    for(int i=0;i<t;i++){
    cin>>n;
    arr = new int[n];
    for(int j=0;j<n;j++)
        cin>>arr[j];
    Sort(arr,n);
    for(int j=0;j<n;j++)
        cout<<arr[j]<<" ";
    cout<<endl; 
    delete[] arr;
    }
 	
 	
 	return 0;
} 

    