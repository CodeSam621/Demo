import { useState, useEffect } from "react";
import { S3Client } from "@aws-sdk/client-s3";
import { Upload } from "@aws-sdk/lib-storage";
import { MdOnlinePrediction } from "react-icons/md";
import './App.css';

const bucketName = "vehicle-image-bucket"
const creds = {
  accessKeyId: "<REPLACE WITH YOUR ACCESS KEY>",  
  secretAccessKey: "<REPLACE WITH YOUR SECRET KEY>",
};

const client = new S3Client({
  region: "ap-southeast-2",  
  signatureVersion: 'v4',
  credentials: creds
});

function App() {
  const [image, setImage] = useState(null);
  const [message, setMessage] = useState("");
  const [ws, setWs] = useState(undefined);
  const [numberPlate, setNumberPlate] = useState("");
  const [socketStatusColour, setSocketStatusColour]= useState("grey")

  useEffect(() => {
    if(!ws){
      console.log('........Connecting to server...........')
      const webSocket = new WebSocket("wss://nb1t7abol1.execute-api.us-east-1.amazonaws.com/dev/");
      setWs(webSocket)     
    } else{
      setSocketStatusColour("grey")
    }
  },[]);


  if(ws) {
    ws.onopen = (event) => {
      console.log('Connection established', event)
      setSocketStatusColour("green")
    };
    ws.onmessage = function (event) {
      console.log(`event`, event)      
      try {     
        const data = JSON.parse(event.data);
          console.log('Number:', data.message)
          setMessage("")
          setNumberPlate(`Number plate: ${data.message}`);

      } catch (err) {
        console.log(err);
      }
    };  
  }

  const processImage = async (event) => {
      setNumberPlate(`Number plate: .....`);
      setImage(event.target.files[0])

      const uploadResult = await uploadFileToS3(event.target.files[0])
      if(uploadResult){
        const imageName = event.target.files[0].name;
        await sendMessage(imageName);
      }
  }

  const uploadFileToS3 = async(image) => {
    setMessage("Uploading......")
    const target = { Bucket: bucketName, Key: image.name, Body: image };
    try {
      const parallelUploads3 = new Upload({
        client: client,
        // tags: [{ Key: "connection_id", Value: "123"}], // optional tags
        queueSize: 4, // optional concurrency configuration
        leavePartsOnError: false, // optional manually handle dropped parts
        params: target,
      });

      parallelUploads3.on("httpUploadProgress", (progress) => {
        console.log("progress:", progress);
      });

      var result = await parallelUploads3.done();

      setMessage("Upload is done")

      // console.log('Result:', result);
      return true;

    } catch (e) {
      console.log(e);
      setMessage("Upload is failed");
    }
    return false;
  }

  const sendMessage = async (imageName) => {
    try {
      if(ws) {
        setMessage(`Sending image ${imageName} info....`)

       const result =  await ws.send( JSON.stringify( {
          "action": "sendVehicleInfo",
          "message": {"bucket": bucketName, "key": imageName}
      }));

      console.log('result', result)
        setMessage("Processing image....")
      }    
    }
    catch(err){
      console.log("error", err)
    }
  
  }

  return (
    <div className="App">
      <header className="App-header">
        <h3>Vehicle Number Plate Recognition System</h3>
        <div id="web-socket-status"> <MdOnlinePrediction color= {socketStatusColour} size={100} /></div>
        {
          image=== null? <div></div>:<img src={URL.createObjectURL(image)} style={{ height: 400, width: 400 }} />
        }
      
      <br></br>
      <input type="file" onChange={processImage} />
      <hr />
      <label id="message">{message}</label>
      <label id="numberPlate">{numberPlate}</label>
      </header>
    </div>
  );
}

export default App;
