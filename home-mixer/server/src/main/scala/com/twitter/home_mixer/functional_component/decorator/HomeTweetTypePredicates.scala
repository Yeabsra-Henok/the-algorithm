package com.twitter.home_mixer.functional_component.decorator

import com.twitter.conversions.DurationOps._
import com.twitter.home_mixer.model.HomeFeatures._
import com.twitter.product_mixer.core.feature.featuremap.FeatureMap
import com.twitter.timelinemixer.injection.model.candidate.SemanticCoreFeatures
import com.twitter.tweetypie.{thriftscala => tpt}

object HomeTweetTypePredicates {

  private[this] val CandidatePredicates: Seq[(String, FeatureMap => Boolean)] = Seq(
    ("with_candidate", _ => true),
    ("retweet", _.getOrElse(IsRetweetFeature, false)),
    ("reply", _.getOrElse(InReplyToTweetIdFeature, None).nonEmpty),
    ("image", _.getOrElse(EarlybirdFeature, None).exists(_.hasImage)),
    ("video", _.getOrElse(EarlybirdFeature, None).exists(_.hasVideo)),
    ("link", _.getOrElse(EarlybirdFeature, None).exists(_.hasVisibleLink)),
    ("quote", _.getOrElse(EarlybirdFeature, None).exists(_.hasQuote.contains(true))),
    ("like_social_context", _.getOrElse(NonSelfFavoritedByUserIdsFeature, Seq.empty).nonEmpty),
    ("has_scheduled_space", _.getOrElse(AudioSpaceMetaDataFeature, None).exists(_.isScheduled)),
    ("has_recorded_space", _.getOrElse(AudioSpaceMetaDataFeature, None).exists(_.isRecorded)),
    ("is_read_from_cache", _.getOrElse(IsReadFromCacheFeature, false)),
    ("get_initial", _.getOrElse(GetInitialFeature, false)),
    ("get_newer", _.getOrElse(GetNewerFeature, false)),
    ("get_middle", _.getOrElse(GetMiddleFeature, false)),
    ("get_older", _.getOrElse(GetOlderFeature, false)),
    ("polling", _.getOrElse(PollingFeature, false)),
    ("empty_request", _ => false),
    ("authored_by_contextual_user", _.getOrElse(AuthoredByContextualUserFeature, false)),
    ("has_ancestors", _.getOrElse(AncestorsFeature, Seq.empty).nonEmpty),
    ("full_scoring_succeeded", _.getOrElse(FullScoringSucceededFeature, false)),
    ("has_semantic_core_annotation", _.getOrElse(EarlybirdFeature, None).exists(_.semanticCoreAnnotations.nonEmpty)),
    ("is_request_context_foreground", _.getOrElse(IsRequestContextForegroundFeature, false))
  )
}
