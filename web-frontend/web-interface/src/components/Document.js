import React, {useEffect, useState} from 'react';

const Document = (props) => {
    const [tableRows, setRows] = useState([]);

    useEffect(() => {
        let sketch_rows = {};
        let doc = props.doc;
        let sketch = props.sketch;

        for (let obj of sketch) {
            let start = obj['start'];
            let end = obj['end'];
            let topic = obj['topic'];
            for (let i = start; i <= end; i += 1) {
                if (sketch_rows[i] == null) {
                    sketch_rows[i] = [];
                }
                sketch_rows[i].push("'" + topic + "'");
            }
        }
        
        let rows = [];
        // headers
        let headers_cell = []
        headers_cell.push(<td key={"cell000"} id={"cell000"} style={{padding: 8, fontWeight: 700}}>#</td>)
        headers_cell.push(<td key={"cell001"} id={"cell001"} style={{padding: 8, fontWeight: 700}}>Sentence</td>)
        headers_cell.push(<td key={"cell002"} id={"cell002"} style={{padding: 8, paddingLeft: 32, fontWeight: 700}}>Sketch Topics</td>)
        rows.push(<tr key={-1} id={"row00"}>{headers_cell}</tr>)

        // data
        for (var i = 0; i < doc.length; i++){
          let rowID = `row${i}`;
          let cell = [];
          for (var idx = 0; idx < 3; idx++){
            let cellID = `cell${i}-${idx}`
            if (idx === 0) {
                cell.push(<td key={cellID} id={cellID} style={{padding: 8, wordWrap: 'break-word', width: "0.1%"}}>[{i}]</td>);
            } else if (idx === 1) {
                cell.push(<td key={cellID} id={cellID} style={{padding: 8, wordWrap: 'break-word', width: "15%" }}>{doc[i]}</td>);
            } else if (idx === 2) {
                cell.push(<td key={cellID} id={cellID} style={{padding: 8, wordWrap: 'break-word', width: "15%", addingLeft: 32, fontStyle: "italic"}}>
                    {sketch_rows[i] ? sketch_rows[i].join(', ') : null}
                </td>);
            }
          }
          rows.push(<tr key={i} id={rowID}>{cell}</tr>);
        }
        setRows(rows);
    }, [props.doc, props.sketch])

    return (
        <div style={{padding: 32, margin: 32, width: "100%"}}>
            {props.doc.length === 0 || !tableRows ? "No document yet."
                :
                <div className="container" style={{fontSize: "x-large"}}>
                    <div className="row">
                        <div className="col s12 board">
                            <table id="simple-board">
                                <tbody>
                                {tableRows}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            }
        </div>
    );
  }
  
export default Document;
  