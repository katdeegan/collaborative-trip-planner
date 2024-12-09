# Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Testing Locally

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## Deploying frontend

This directory contain the code for the **collaboartive-trip-planner** service's frontend (a React application).

Once the backend services have all been provisioned and deployed, the **userServerHost** and **tripServerHost** constants in the **App.js** file should be updated to point to the correct IP addresses for each service. If running the React frontend in the same Kubernetes cluster as the **User and Trip Servers**, the respective service names may be used (as defined in each server's service.yaml file). Otherwise, these constants should point the the EXTERNAL_IP addresses of the services.


### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

Once the React app has been built successfully, the following terminal commands can be used to deploy to Kubernetes:

```bash
kubectl apply -f frontend/deployment.yaml

kubectl apply -f frontend/service.yaml
```


As configured, these commands will provision a Kubernetes pod to host the frontend (number of pods can be scaled based on application needs), and a Load Balancer service.

The entire application may then be accessed by navigating to the react-frontend-service's EXTERNAL-IP, which may be found be executing the **kubectl get svc** command within your Kubernetes environment.

