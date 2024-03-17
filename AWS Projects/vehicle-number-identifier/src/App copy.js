import React from "react";
import {S3} from "@aws-sdk/client-s3";
import './App.css';

const s3 = new S3({region: 'ap-southeast-2'});

function App2() {
  const [myimage, setMyImage] = React.useState(null);
  const uploadImage = e => {
    console.log('e:', e.target.files[0])

    setMyImage(URL.createObjectURL(e.target.files[0]));
    uploadFileToS3()
  };

  const uploadFileToS3 = async() => {
    const S3_BUCKET = "bucket-name";
    // S3 Region
    // const REGION = "region";

    // S3 Credentials
    // AWS.config.update({
    //   accessKeyId: "youraccesskeyhere",
    //   secretAccessKey: "yoursecretaccesskeyhere",
    // });
    const s3 = new AWS.S3({
      params: { Bucket: S3_BUCKET },
      // region: REGION,
    });

    // Files Parameters

    const params = {
      Bucket: S3_BUCKET,
      Key: "myimage.name",
      Body: myimage,
    };

    // Uploading file to s3

    var upload = s3
      .putObject(params)
      .on("httpUploadProgress", (evt) => {
        // File uploading progress
        console.log(
          "Uploading " + parseInt((evt.loaded * 100) / evt.total) + "%"
        );
      })
      .promise();

    await upload.then((err, data) => {
      console.log(err);
      // Fille successfully uploaded
      alert("File uploaded successfully.");
    });
  }

  return (
    <div className="App">
      <header className="App-header">
      <img src={myimage} style={{ height: 200, width: 200 }} />
      
      <br></br>
      <input type="file" onChange={uploadImage} />
      <hr />
      </header>
    </div>
  );
}

export default App;