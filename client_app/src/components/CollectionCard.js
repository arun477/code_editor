import React from 'react';
import './collectionCard.css';

const CollectionCard = ({ title, bannerImg, description, onClick }) => {
  return (
    <div className="banner-card">
      <img src={bannerImg} alt={title} className="banner-img" />
      <div className="banner-content">
        <h2 className="banner-title">{title}</h2>
        <p className="banner-description">{description}</p>
      </div>
      {/* <button className="banner-btn" onClick={onClick}>
        Start
      </button> */}
    </div>
  );
};

export default CollectionCard;