export function Review(props) {
    return (<div>
        <b>Movie ID: {props.movieID} </b>
        <input type="number" onChange={props.onRate} value={props.rating} min="1" max="5"/>
        <input value={props.comment} onChange={props.onEdit}/>
        <button onClick={props.onDelete}>Delete</button>
    </div>);
}