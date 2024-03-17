import { useState, useEffect } from "react";
import { S3Client } from "@aws-sdk/client-s3";
import { Upload } from "@aws-sdk/lib-storage";
import './App.css';

const bucketName = "vehicle-image-bucket"
const creds = {
  accessKeyId: "xxxxxxx", // replace with access Id
  secretAccessKey: "xxxxxx", // replace with secret key
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
  const [numberPlate, setNumberPlate] = useState("Number plate:.......");

  useEffect(() => {
    if(!ws){
      console.log('........Connecting to server...........')
      const webSocket = new WebSocket("wss://car8br8gbh.execute-api.ap-southeast-2.amazonaws.com/dev/");
      setWs(webSocket)
    }  
  },[]);

  if(ws) {
    ws.onopen = (event) => {
      console.log('Connection established', event)
    };
    ws.onmessage = function (event) {
      console.log(`event`, event)      
      try {     
        const data = JSON.parse(event.data);
          console.log('data', data.message)
          setMessage("")
          setNumberPlate(`Number plate: ${data.message}`);

      } catch (err) {
        console.log(err);
      }
    };  
  }

  const processImage = async (e) => {
      setNumberPlate(`Number plate: .....`);
      const imageName = e.target.files[0].name;
      setImage(e.target.files[0])

      const uploadResult = await uploadFileToS3(e.target.files[0])
      if(uploadResult){
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
    try{
      if(ws) {
        setMessage(`Sending image ${imageName} info....`)

        await ws.send( JSON.stringify( {
          "action": "send",
          "message": {"bucket": bucketName, "key": imageName}
      }));
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
      <img src={image == null? "https://placehold.jp/150x150.png": URL.createObjectURL(image)} style={{ height: 400, width: 400 }} />
      
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