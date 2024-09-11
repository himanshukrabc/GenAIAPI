import './Card.css';

function Card(props) {
    function handleAction(action) {
        if (props.onAction) {
            props.onAction(action);
        }
    }

    return <div className="card">
        <ul>
            <div className="header">This is a React component</div>
            {props.cards.map((card, index) =>
                <li className="card-item" key={index}>
                    <div className='card-info'>
                        <img className='card-image' src={card.imageUrl} alt="Card"></img>
                        <div className='info'>
                            <div className='title'>{card.title}</div>
                            <div className='actions'>
                                {card.actions.map((action, index) =>
                                    <button key={index} onClick={(e) => handleAction(action, e)}>{action.label}</button>
                                )}
                            </div>
                        </div>
                    </div>
                </li>
            )}
        </ul>
    </div>;
}

export default Card;