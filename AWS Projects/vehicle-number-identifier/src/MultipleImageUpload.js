import React from "react";
const dummy = "https://static.thenounproject.com/png/625182-200.png";
class MultipleImageUpload extends React.Component {
  state = { current: null, old: [] };
  uploadImage = e => {
    const { current, old } = this.state;

    this.setState(
      {
        current: URL.createObjectURL(e.target.files[0])
      },
      () => {
        this.setState({ old: [...old, current] });
      }
    );

    this.setState({ current: URL.createObjectURL(e.target.files[0]) });
  };
  render() {
    console.log(this.state);
    const { old, current } = this.state;
    return (
      <div className="App">
        {/* <div>
          <h3>Current</h3>
          <img
            src={current ? current : dummy}
            alt="custom-pic"
            style={{ height: 100, width: 100 }}
          />
        </div> */}
        <hr />
        {/* {old
          ? old.map((o, i) => (
              <img
                src={o ? o : dummy}
                key={i.toString()}
                alt="preview"
                style={{ height: 100, width: 100 }}
              />
            ))
          : ""} */}

        <input type="file" onChange={this.uploadImage} />
      </div>
    );
  }
}
export default MultipleImageUpload;
