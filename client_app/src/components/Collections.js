import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import Styles from './problemList.module.css';
import Loader from './Loader';
import CollectionCard from './CollectionCard';
import { useApi } from '../utils/api';
import { API_BASE_URL } from '../constants';

function Collections() {
    const [collections, setCollections] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const { callApi } = useApi();

    useEffect(() => {
        const fetchCollections = async () => {
            try {
                const data = await callApi('/modules');
                setCollections(data || []);
                setLoading(false);
            } catch (error) {
                console.error('Error fetching collections:', error);
                setError(error.message);
                setLoading(false);
            }
        };

        fetchCollections();
    }, [callApi]);

    if (loading)
        return (
            <div>
                <Loader />
            </div>
        );
    if (error) return <div>Error: {error}</div>;

    return (
        <div className={Styles.parent}>
            <h3 className={Styles.heading}>Modules</h3>
            <ul
                className={Styles.list}
                style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center' }}
            >
                {collections.map((collection) => (
                    <li
                        className={Styles.listItem}
                        key={collection.collectionId}
                        style={{ width: '300px', margin: '10px' }}
                    >
                        <Link
                            className={Styles.link}
                            to={!collection.isLocked ? `/module/${collection.id}` : '/#'}
                            style={{ cursor: !collection.isLocked ? 'pointer' : 'not-allowed' }}
                        >
                            <CollectionCard
                                title={collection.banner_title}
                                bannerImg={`${API_BASE_URL}/${collection.banner_img}`}
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
