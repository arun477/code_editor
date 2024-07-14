import React from 'react';
import './collectionCard.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock, faLockOpen } from '@fortawesome/free-solid-svg-icons';

const CollectionCard = ({ title, bannerImg, description, isLocked }) => {
    return (
        <div className="banner-card">
            <img src={bannerImg} alt={title} className="banner-img" />
            <div className="banner-content">
                <h2 className="banner-title">{title}</h2>
                <p className="banner-description">{description}</p>
            </div>
            <div className='banner-lock-icon-parent'>      <FontAwesomeIcon icon={isLocked?faLock:faLockOpen} style={{ color: '#f5ac0b' }} /></div>

        </div>
    );
};

export default CollectionCard;