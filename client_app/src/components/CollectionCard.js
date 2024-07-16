import React, { useState } from 'react';
import './collectionCard.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faLock, faLockOpen } from '@fortawesome/free-solid-svg-icons';

const CollectionCard = ({ title, bannerImg, description, isLocked }) => {
    const [style, setStyle] = useState({});

    const handleMouseMove = (e) => {
        const card = e.currentTarget;
        const { left, top, width, height } = card.getBoundingClientRect();
        const x = e.clientX - left - width / 2;
        const y = e.clientY - top - height / 2;

        const rotateX = (y / height) * 10;
        const rotateY = (x / width) * -10;

        setStyle({
            transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`,
            transition: 'none'
        });
    };

    const handleMouseLeave = () => {
        setStyle({
            transform: `perspective(1000px) rotateX(0deg) rotateY(0deg)`,
            transition: 'transform 0.5s ease'
        });
    };

    return (
        <div 
            className="banner-card" 
            style={style} 
            onMouseMove={handleMouseMove} 
            onMouseLeave={handleMouseLeave}
        >
            <img src={bannerImg} alt={title} className="banner-img" />
            <div className="banner-content">
                <h2 className="banner-title">{title}</h2>
                <p className="banner-description">{description}</p>
            </div>
            <div className="banner-lock-icon-parent">
                <FontAwesomeIcon icon={isLocked ? faLock : faLockOpen} style={{ color: '#f5ac0b' }} />
            </div>
        </div>
    );
};

export default CollectionCard;
