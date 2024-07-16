import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar } from '@fortawesome/free-solid-svg-icons';
import Styles from './problemList.module.css'
import Loader from './Loader';
import CollectionCard from './CollectionCard';

function Collections() {
    const [collections, setCollections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://localhost:8000/modules')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {

                setCollections(data || []);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching problems:', error);
                setError(error.message);
                setLoading(false);
            });
    }, []);

    if (loading) return <div><Loader /></div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div className={Styles.parent}>
            <h3 className={Styles.heading}>Modules</h3>
            <ul className={Styles.list} style={{display:'flex', flexWrap:'wrap', justifyContent:'center'}}>
                {collections.map(collection => (
                    <li className={Styles.listItem} key={collection.collectionId} style={{ width: '300px', margin: '10px' }}>
                        <Link className={Styles.link} to={!collection.isLocked?`/module/${collection.id}`:'/#'} style={{cursor: !collection.isLocked?'pointer':'not-allowed'}}>
                            <CollectionCard
                                title={collection.banner_title}
                                bannerImg={'http://localhost:8000/' + collection.banner_img}
                                description={collection.banner_description}
                                isLocked={collection.isLocked}
                            />

                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default Collections;
