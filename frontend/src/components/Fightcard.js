import React from 'react';

function Fightcard({ fighter_data }) {
    const { fighter } = fighter_data;
    const { image_url } = fighter;

     // Create a base style
     const baseStyle = {
        backgroundSize: 'contain', 
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat' 
     }
    


  // Conditionally add backgroundImage if image_url exists
  const backgroundImageStyle = image_url
    ? { ...baseStyle, backgroundImage: `url(${image_url})` }
    : baseStyle;

  return (
    <div className="fightcard-container" style={backgroundImageStyle}>
        <div className="fighter-info">
            <div className="fighter-name">
            <div className="first-name">{fighter.name.split(' ')[0]}</div>
            <div className="last-name">{fighter.name.split(' ')[1]}</div>
            {fighter.nickname !== "Unknown" && <div className="nick-name">"{fighter.nickname}"</div>}
            </div>
        </div>

        <div className="fighter-stats">
            <p className="stat">Height: {fighter.height}</p>
            <p className="stat">Reach: {fighter.reach}</p>
            <p className="stat">Weight: {fighter.weight}</p>
            <p className="stat">Wins: {fighter.wins}</p>
            <p className="stat">Losses: {fighter.losses}</p>
            <p className="stat">Draws: {fighter.draws}</p>
            <p className="stat">Stance: {fighter.stance}</p>
        </div>
    </div>
  );
}

export default Fightcard;